import factory

from app.models import Class, Student
from authentication.models import Teacher


PASSWORD = 'testing123'


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    first_name = 'John'
    last_name = factory.Sequence(lambda n: 'Doe_{0}'.format(n))
    username = factory.LazyAttribute(
        lambda obj: '{0}_{1}@test.com'.
        format(obj.first_name.lower(), obj.last_name.lower())
    )
    password = factory.PostGenerationMethodCall(
        'set_password',
        PASSWORD
    )


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    name = factory.Sequence(lambda n: 'class_{0}'.format(n))
    teacher = factory.SubFactory(TeacherFactory)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = 'John'
    middle_name = 'Junior'
    last_name = factory.Sequence(lambda n: 'Doe_{0}'.format(n))
    my_class = factory.SubFactory(ClassFactory)
