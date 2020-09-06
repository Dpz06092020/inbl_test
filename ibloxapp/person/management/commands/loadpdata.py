import json
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import IntegrityError
from person.models import PersonData, Person
from person.validations import person_validation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='JSON File with Full Path')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        with open(filename, encoding='utf-8') as f:
            models = json.load(f)

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
                self.stderr.write('PersonData Creation in DB Failed {id = ' + str(p_id) + '}', e)

            try:
                if save_flag:
                    person_model = Person(id=p_id, first_name=first_name, last_name=last_name,
                                          city=city, data=person_data_model_obj)
                    person_model.save(force_insert=True)
            except IntegrityError as e:
                person_data_model_obj.delete()
                self.stderr.write('Record Creation in DB Failed {id = ' + str(p_id) + '}', e)
            except ValueError as e:
                person_data_model_obj.delete()
                self.stderr.write('Record Creation in DB Failed {id = ' + str(p_id) + '}', e)