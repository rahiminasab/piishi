from django.test import TestCase
from django.contrib import auth
from django.core import mail

from web.backend.registrar.views import *


class LoginTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        pass

    def test_anonymous_visit(self):
        resp = self.client.get('/')
        self.assertRedirects(resp, reverse('login'))

    def test_login_page(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sign In')

    def test_login_action_success(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        garfield = User.objects.get(pk=1)
        garfield.set_password('Meow!Meow')
        garfield.save()

        self.client.login(username=garfield.username, password='Meow!Meow')

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_login_action_failure(self):
        garfield = User.objects.get(pk=1)
        garfield.set_password('Meow!Meow')
        garfield.save()

        self.client.login(username=garfield.username, password='wrongPass')

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        resp = self.client.get('/')
        self.assertRedirects(resp, reverse('login'))


class SignUpTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        pass

    def test_sign_up_page(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sign Up')

    def test_sign_up_form_valid(self):
        form = SignUpForm(data={"first_name": "Cathlene", "last_name": "Caterpillar",
                                "username": "cathlene", "email": "cathlene@piishi.com",
                                "password1": "Meow!Meow", "password2": "Meow!Meow"})
        self.assertTrue(form.is_valid())

    def test_sign_up_form_user_already_exists(self):
        form = SignUpForm(data={"first_name": "Cathlene", "last_name": "Caterpillar",
                                "username": "garfield", "email": "cathlene@piishi.com",
                                "password1": "Meow!Meow", "password2": "Meow!Meow"})
        self.assertFalse(form.is_valid())
        self.assertTrue('username already taken' in str(form.errors))

    def test_sign_up_form_email_not_unique(self):
        form = SignUpForm(data={"first_name": "Cathlene", "last_name": "Caterpillar",
                                "username": "cathlene", "email": "piishi.com@gmail.com",
                                "password1": "Meow!Meow", "password2": "Meow!Meow"})
        self.assertFalse(form.is_valid())
        self.assertTrue('this email is already associated with an account' in str(form.errors))

    def test_sign_up_form_pass_mismatch(self):
        form = SignUpForm(data={"first_name": "Cathlene", "last_name": "Caterpillar",
                                "username": "cathlene", "email": "cathlene@piishi.com",
                                "password1": "Meow!Meow", "password2": "D@ssw0rd"})
        self.assertFalse(form.is_valid())
        self.assertTrue('The two password fields didn&#39;t match.' in str(form.errors))

    def test_user_signup_action(self):
        resp = self.client.post(reverse('signup'), {"first_name": "Cathlene", "last_name": "Caterpillar",
                                                    "username": "cathlene", "email": "cathlene@piishi.com",
                                                    "password1": "Meow!Meow", "password2": "Meow!Meow"}, follow=True)
        self.assertRedirects(resp, reverse('user_activation_pending', kwargs={'email': 'cathlene@piishi.com'}))
        self.assertTemplateUsed(resp, 'registration/activation/user_activation_pending.html')

        user = User.objects.get(username='cathlene')

        self.assertTrue(user.first_name, "Cathlene")
        self.assertTrue(user.last_name, "Caterpillar")
        self.assertTrue(user.email, "cathlene@piishi.com")
        self.assertFalse(user.is_active)

    def test_user_activation_done(self):
        self.client.post(reverse('signup'), {"first_name": "Cathlene", "last_name": "Caterpillar",
                                             "username": "cathlene", "email": "cathlene@piishi.com",
                                             "password1": "Meow!Meow", "password2": "Meow!Meow"}, follow=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Please activate your account at Piishi.com')
        self.assertTrue('Thanks for signing up at Piishi!' in mail.outbox[0].body)
        import re
        urls = re.findall('http://.*/', mail.outbox[0].body)
        self.assertEqual(len(urls), 1)
        resp = self.client.get(urls[0])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/activation/user_activation_done.html')

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        cathlene = User.objects.get(username='cathlene')
        self.assertTrue(cathlene.is_active)

        self.assertEqual(user, cathlene)

    def test_user_activation_done_invalid_link(self):
        resp = self.client.post(reverse('user_activation_done',
                                        kwargs={"uidb64": "NA", "token": "4xz-243b5b358ed4436fff50"}))
        self.assertContains(resp, "Activation link is invalid!")


class LogoutTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        pass

    def test_logout_page(self):
        resp = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(resp, reverse('login'))

    def test_logout_user(self):
        garfield = User.objects.get(pk=1)
        garfield.set_password('Meow!Meow')
        garfield.save()

        self.client.login(username=garfield.username, password='Meow!Meow')

        resp = self.client.get(reverse('home'))

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertContains(resp, reverse('logout'))

        self.client.get(reverse('logout'))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        resp = self.client.get(reverse('home'), follow=True)
        self.assertNotContains(resp, reverse('logout'))


class ResetPassTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.garfield = User.objects.get(pk=1)
        self.garfield.email = 'abc@def.com'
        self.garfield.set_password('Meow!Meow')
        self.garfield.save()

    def test_sign_in_page_has_pass_reset_link(self):
        resp = self.client.get(reverse('login'))
        self.assertContains(resp, reverse('reset_pass_submit'))

    def test_pass_reset_init_form(self):
        form = ResetPassInitForm(data={"email_input": 'no_such_email@piishi.com'})
        self.assertFalse(form.is_valid())
        self.assertTrue('User with this Email address is not found!'in str(form.errors))

    def test_pass_reset_confirm_form(self):
        form = ResetPassConfirmForm(data={"password": "Meow!Meow", "password_repeat": "Meow!Meow"})
        self.assertTrue(form.is_valid())

        form = ResetPassConfirmForm(data={"password": "Meow!Meow", "password_repeat": "Another"})
        self.assertFalse(form.is_valid())

    def test_pass_reset_functionality(self):
        resp = self.client.get(reverse('reset_pass_submit'))
        self.assertTemplateUsed(resp, 'registration/reset_pass/reset_pass_init.html')

        resp = self.client.post(reverse('reset_pass_submit'), {"email_input": self.garfield.email}, follow=True)
        self.assertTemplateUsed(resp, 'registration/reset_pass/reset_pass_pending.html')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset request at piishi.com')
        self.assertTrue('We have received a password reset request for your account at piishi.com'
                        in mail.outbox[0].body)
        import re
        urls = re.findall('http://.*/', mail.outbox[0].body)
        self.assertEqual(len(urls), 1)
        resp = self.client.get(urls[0])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/reset_pass/reset_pass_confirm.html')

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user, self.garfield)

        resp = self.client.post(reverse('reset_pass_done'),
                                {"password": "AnotherPass123", "password_repeat": "AnotherPass123"}, follow=True)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/reset_pass/reset_pass_done.html')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user, self.garfield)

        self.garfield.refresh_from_db()
        self.assertTrue(self.garfield.check_password("AnotherPass123"))

    def test_reset_pass_confirm_invalid_link(self):
        resp = self.client.post(reverse('reset_pass_confirm',
                                kwargs={"uidb64": "NA", "token": "4xz-243b5b358ed4436fff50"}))
        self.assertContains(resp, "reset pass link is invalid!")
