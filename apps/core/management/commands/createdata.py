from django.core.management import BaseCommand, call_command

__author__ = 'phillip'


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command(
            'dumpdata',
            #Taxonomy
            'taxonomy.Term',
            'taxonomy.Taxonomy',

            #Community
            'community.Community',

            #Company
            'company.CompanyContactType',
            'company.Company',

            #UserPRofile
            'userprofile.Responsibility',

            #ContentTypes
            'contenttypes.ContentType',

            #JobVacancy
            'job_vacancy.WorkLoad',
            'job_vacancy.SalaryType',
            'job_vacancy.Level',
            'job_vacancy.JobVacancyResponsibilityType',
            'job_vacancy.Benefit',
            'job_vacancy.JobRegime',
            'job_vacancy.Experience',
            'job_vacancy.Exigency',

            #Geograph
            'geography.Country',
            'geography.State',
            'geography.City',

            #Contact
            'contact.ContactSubject',

            #Config
            'configuration.ConfigGroup',
            'configuration.ConfigKey',

            #Complaint
            'complaint.ComplaintType',

            #OUTPUT
            output='apps/core/fixtures/initial_data.json'
        )