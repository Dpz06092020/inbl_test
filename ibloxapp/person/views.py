import json
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from person.forms import CreateUserForm
from person.models import PersonData, Person
from person.serializers import FetchPersonSerializer
from person.validations import person_validation
import logging

logger = logging.getLogger('iblox.logger')
JSON_PARAMS = {'indent': 2}


def landing_view(request):
    logger.info("Home Page Accessed: /")
    return HttpResponse("<h1>HelloWorld!</h1>")


@csrf_exempt
@api_view(['POST', ])
def register_view(request):
    try:
        request_data = json.loads(request.body)
        logger.info("Register API Accessed: /")
        form = CreateUserForm(request_data)
        if form.is_valid():
            form.save()
            return HttpResponse('User Registered')
        else:
            msg = []
            for m in form.errors:
                msg.append(m)
            logger.error('Error in Registration : ' + ','.join(msg))
            return HttpResponse('Error in Registration: ' + ','.join(msg))
    except json.decoder.JSONDecodeError as e:
        logger.error('Error in Registration : Malformed Request Body ' + str(e.args[0]))
        return HttpResponse('Malformed request body ' + str(e.args[0]))


@csrf_exempt
@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def add_person_view(request):
    """
    Function to add new Person
    """
    # Predefined structure for response object.
    response_data = {'status': '', 'code': None, 'message': None, 'data': []}
    logger.info('Person Creation Endpoint Accessed : /api/new')
    if request.method == 'PUT':
        try:
            models = json.loads(request.body)
            # Verify all data before Insertion, Fail if any one data is corrupted
            record_count = 0
            for m in models:
                record_count = record_count + 1
                valid_status = person_validation.validate_add(m)
                if not valid_status[0]:
                    raise ValidationError(valid_status[1])

            for person in models:
                person_data = person.get('data')[0]
                enabled = person_data.get('enabled')
                guid = person_data.get('guid')
                first_name = person.get('first_name')
                last_name = person.get('last_name')
                city = person.get('city')
                p_id = person.get('id')

                person_data_model_obj = PersonData(enabled=enabled, guid=guid)
                save_flag = True
                try:
                    person_data_model_obj.save()
                except ValueError as e:
                    save_flag = False
                    person_data_model_obj.delete()
                    response_data['status'] = False
                    response_data['code'] = 500
                    response_data['message'] = 'PersonData Creation in DB Failed {id = ' + str(p_id) + '}'
                    logger.error('PersonData Creation in DB Failed {id = ' + str(p_id) + '}')

                try:
                    if save_flag:
                        person_model = Person(id=p_id, first_name=first_name, last_name=last_name,
                                              city=city, data=person_data_model_obj)
                        person_model.save(force_insert=True)
                        response_data['status'] = True
                        response_data['code'] = 200
                        response_data['message'] = 'Data Creation Success, id=' + str(p_id)
                        response_data['data'] = []
                        logger.info('Person Record Created Successfully : id=' + str(p_id))

                except IntegrityError as e:
                    person_data_model_obj.delete()
                    response_data['status'] = False
                    response_data['code'] = 500
                    response_data['message'] = 'Record Creation in DB Failed {id = ' + str(p_id) + '}'
                    logger.error('PersonData Creation in DB Failed {id = ' + str(p_id) + '}',e)
                except ValueError as e:
                    person_data_model_obj.delete()
                    response_data['status'] = False
                    response_data['code'] = 500
                    response_data['message'] = 'Record Creation in DB Failed {id = ' + str(p_id) + '}'
                    logger.error('PersonData Creation in DB Failed {id = ' + str(p_id) + '}', e)
        except ValidationError as e:
            response_data['status'] = False
            response_data['code'] = 400
            response_data['message'] = e.args[0]
            logger.error('PersonData Validation Failed in /api/new ' + str(e.args[0]), e)

        except JSONDecodeError as e:
            response_data['status'] = False
            response_data['code'] = 400
            response_data['message'] = "JSON Error = " + str(e.args[0])
            logger.error('JSON Decode Error in /api/new', e)
    else:
        response_data['status'] = False
        response_data['code'] = 400  # Bad Request
        response_data['message'] = "Method not supported"
        response_data['data'] = []
        logger.error('Method not Supported in /api/new')

    return JsonResponse(response_data, json_dumps_params=JSON_PARAMS)


@permission_classes([IsAuthenticated])
class FetchAll(ListAPIView):
    queryset = Person.objects.all().filter(data__enabled=True).order_by("id")
    pagination_class = PageNumberPagination
    serializer_class = FetchPersonSerializer


# Normal Get Without Pagination
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_all_persons_view(request):
    """
        Function to get all Person models
    """
    response_data = {'status': '', 'code': None, 'message': None, 'data': []}
    if request.method == 'GET':
        try:
            model_obj = Person.objects.all().filter(data__enabled=True).order_by("id")
            data = []
            for obj in model_obj:
                data.append(obj.get_dict())
            # If no exception, response object is populated as success
            response_data['status'] = True
            response_data['code'] = 200  # Sucess
            response_data['message'] = "OK"
            response_data['data'].append(data)
        except IntegrityError as e:
            response_data['status'] = False
            response_data['code'] = 400  # Bad Request
            response_data['message'] = "Integrity Exception Occurred"
            response_data['data'] = []
    else:
        response_data['status'] = False
        response_data['code'] = 404  # Bad Request
        response_data['message'] = "Method not supported"
        response_data['data'] = []

    return JsonResponse(response_data, json_dumps_params=JSON_PARAMS)

