import factory

from authentication.models import Teacher


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    first_name = 'John'
    last_name = factory.Sequence(lambda n: 'Doe{0}'.format(n))
    username = factory.LazyAttribute(
        lambda obj: '{0}_{1}@test.com'.
        format(obj.first_name.lower(), obj.last_name.lower())
    )
    password = 'testing123'
