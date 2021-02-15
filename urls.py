from Download import views
from django.conf.urls import url
from .middlewares.login_required_middleware import login_required
from .middlewares.cannot_access_after_login import cantAccessAfterLogin

urlpatterns = [
url('home',views.homepage),
url('login',cantAccessAfterLogin(views.loginpage)),
url('show',views.showpage),
url('signup',cantAccessAfterLogin(views.signuppage)),
url('verify',cantAccessAfterLogin(views.emailverifypage)),
url('email-verified',cantAccessAfterLogin(views.page_afterverification)),
url('Logout',views.logout),
url('free-download',login_required(views.freedownloadpage)),
url('create-payment',login_required(views.downloadrequestpage)),
url('complete-payment',login_required(views.completepaymentpage)),
url('download-paid-product',login_required(views.downloadAfterpayment)),
url('myorder',login_required(views.OrderPage)),
url('forgot-password',views.forgotpasswordpage),
url('ResetpasswordthroughEmail',views.VerifyEmailForResetPassword),
url('change-password',views.ChangePassword)
]
