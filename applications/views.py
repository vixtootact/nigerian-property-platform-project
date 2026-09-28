from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

from .models import Application
from properties.models import Property

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def submit_application(request):
    try:
        data        = request.data
        property_id = data.get('property_id')
        tenant_id   = data.get('tenant_id')
        message     = data.get('message', '')

        if not property_id or not tenant_id:
            return Response(
                {'error': 'Property ID and Tenant ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            property = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=404)

        if property.status != 'available':
            return Response(
                {'error': 'This property is no longer available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        already_applied = Application.objects.filter(
            property_id=property_id,
            tenant_id=tenant_id
        ).exists()

        if already_applied:
            return Response(
                {'error': 'You have already applied for this property'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application = Application.objects.create(
            property_id = property_id,
            tenant_id   = tenant_id,
            message     = message
        )

        logger.info(f"Application submitted: tenant {tenant_id} for property {property_id}")

        return Response({
            'message': 'Application submitted successfully',
            'application_id': application.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def tenant_applications(request, tenant_id):
    try:
        applications = Application.objects.filter(
            tenant_id=tenant_id
        ).order_by('-applied_at')

        data = [a.to_dict() for a in applications]
        return Response({'applications': data, 'count': len(data)})

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def landlord_applications(request, landlord_id):
    try:
        applications = Application.objects.filter(
            property__landlord_id=landlord_id
        ).order_by('-applied_at')

        data = [a.to_dict() for a in applications]
        return Response({'applications': data, 'count': len(data)})

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['PUT'])
def update_application(request, app_id):
    try:
        application = Application.objects.get(id=app_id)
        new_status  = request.data.get('status')

        if new_status not in ['approved', 'rejected']:
            return Response(
                {'error': 'Status must be approved or rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        if new_status == 'approved':
            application.property.status = 'rented'
            application.property.save()

        logger.info(f"Application {app_id} {new_status}")

        return Response({'message': f'Application {new_status} successfully'})

    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)