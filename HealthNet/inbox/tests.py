from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse_lazy
from .models import Inbox
from core.models import User


class SendMessage(TestCase):

    def test_valid(self):
        from .forms import MessageForm

        user1 = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        user2 = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        user1.save()
        user2.save()

        data = {
            'sender': user1.id,
            'receiver': user2.id,
            'message': 'Hello',
        }
        form = MessageForm(data=data, user=user1)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(Inbox.objects.get(id=instance.id), instance)


"""
def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class DeleteMessage(TestCase):

    def test_valid(self):
        from .forms import MessageForm, DeleteForm
        self.client = Client()
        user1 = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        user2 = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        user1.save()
        user2.save()
        self.client.login(username='test@test.com', password='123pass321pass')
        data = {
            'sender': user1.id,
            'receiver': user2.id,
            'message': 'Hello',
        }
        form = MessageForm(data=data, user=user1)
        form.save()

        request = RequestFactory().get('')
        view = DeleteMessageView()
        view = setup_view(view, request, name=name)
        form2 = DeleteForm(data=data, receiver=user1, sender=user2)
        form2.save()
        import pdb;pdb.set_trace()
        form3 = DeleteForm(data=data, receiver=user1, sender=user2)
        form3.save()
        self.assertFalse(Inbox.objects.filter(id=1).exists())
"""

