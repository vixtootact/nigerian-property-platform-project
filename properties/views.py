from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import csv
import logging

from .models import Property

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['GET', 'POST'])
def property_list(request):
    if request.method == 'GET':
        try:
            search      = request.GET.get('search',    '')
            state       = request.GET.get('state',     '')
            prop_type   = request.GET.get('type',      '')
            min_price   = request.GET.get('min_price', 0)
            max_price   = request.GET.get('max_price', 999999999)
            prop_status = request.GET.get('status',    '')

            properties = Property.objects.all()

            if search:
                from django.db.models import Q
                properties = properties.filter(
                    Q(title__icontains=search) |
                    Q(location__icontains=search) |
                    Q(description__icontains=search)
                )
            if state:
                properties = properties.filter(state=state)
            if prop_type:
                properties = properties.filter(property_type=prop_type)
            if prop_status:
                properties = properties.filter(status=prop_status)

            properties = properties.filter(
                price__gte=float(min_price),
                price__lte=float(max_price)
            )

            properties = properties.order_by('-created_at')

            data = [p.to_dict() for p in properties]

            return Response({'properties': data, 'count': len(data)})

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = request.data

            duplicate = Property.objects.filter(
                landlord_id=data.get('landlord_id'),
                location=data.get('location'),
                property_type=data.get('property_type'),
                price=data.get('price')
            ).exists()

            if duplicate:
                return Response(
                    {'error': 'You already have a similar property in this location'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            property = Property.objects.create(
                title         = data.get('title'),
                description   = data.get('description', ''),
                property_type = data.get('property_type'),
                location      = data.get('location'),
                state         = data.get('state'),
                lga           = data.get('lga', ''),
                price         = float(data.get('price', 0)),
                bedrooms      = int(data.get('bedrooms', 0)),
                bathrooms     = int(data.get('bathrooms', 0)),
                landlord_id   = data.get('landlord_id'),
                image_url     = data.get('image_url', '')
            )

            logger.info(f"New property added: {property.title}")

            return Response({
                'message': 'Property listed successfully',
                'property_id': property.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def property_detail(request, property_id):
    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response({'error': 'Property not found'}, status=404)

    if request.method == 'GET':
        return Response({'property': property.to_dict()})

    elif request.method == 'PUT':
        data = request.data
        property.title         = data.get('title',         property.title)
        property.description   = data.get('description',   property.description)
        property.property_type = data.get('property_type', property.property_type)
        property.location      = data.get('location',      property.location)
        property.state         = data.get('state',         property.state)
        property.lga           = data.get('lga',           property.lga)
        property.price         = float(data.get('price',   property.price))
        property.bedrooms      = int(data.get('bedrooms',  property.bedrooms))
        property.bathrooms     = int(data.get('bathrooms', property.bathrooms))
        property.status        = data.get('status',        property.status)
        property.image_url     = data.get('image_url',     property.image_url)
        property.save()

        logger.info(f"Property updated: {property.title}")
        return Response({'message': 'Property updated successfully'})

    elif request.method == 'DELETE':
        title = property.title
        property.delete()
        logger.info(f"Property deleted: {title}")
        return Response({'message': 'Property deleted successfully'})


@api_view(['GET'])
def landlord_properties(request, landlord_id):
    try:
        properties = Property.objects.filter(
            landlord_id=landlord_id
        ).order_by('-created_at')

        data = [p.to_dict() for p in properties]
        return Response({'properties': data, 'count': len(data)})

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def property_stats(request):
    try:
        from django.db.models import Count, Avg

        total = Property.objects.count()

        by_type = list(
            Property.objects.values('property_type')
            .annotate(count=Count('id'))
        )

        by_state = list(
            Property.objects.values('state')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        by_status = list(
            Property.objects.values('status')
            .annotate(count=Count('id'))
        )

        avg_price = list(
            Property.objects.values('state')
            .annotate(avg_price=Avg('price'))
        )

        return Response({
            'total_properties':   total,
            'by_type':            by_type,
            'by_state':           by_state,
            'by_status':          by_status,
            'avg_price_by_state': avg_price
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def export_csv(request):
    try:
        properties = Property.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="properties.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'ID', 'Title', 'Type', 'Location', 'State',
            'LGA', 'Price (NGN)', 'Bedrooms', 'Bathrooms',
            'Status', 'Date Listed'
        ])

        for p in properties:
            writer.writerow([
                p.id, p.title, p.property_type, p.location,
                p.state, p.lga, p.price, p.bedrooms,
                p.bathrooms, p.status, p.created_at
            ])

        return response

    except Exception as e:
        return Response({'error': str(e)}, status=500)