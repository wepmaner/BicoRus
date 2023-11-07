import pyotp
import qrcode
from qrcode.image.pure import PymagingImage
import uuid
from .models import UserTotp

#генерация секретного ключа, а так же qrcode
def otp_send(request) -> dict:
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key)
    username = request.user.username
    provisioning_uri = totp.provisioning_uri(name=username, issuer_name="BicoRus")
    img = qrcode.make(provisioning_uri, image_factory=PymagingImage)
    filename = f"qrcode/{uuid.uuid4()}.png"
    img.save('media/'+filename)

    request.session['otp_secret_key'] = secret_key
    request.session['file_url'] = filename
    return True

def otp_verify(request,code:int)-> bool:
    secret_key = request.session['otp_secret_key']
    totp = pyotp.TOTP(secret_key)
    
    UserTotp(user=request.user,secret_key=secret_key)
    return totp.verify(code)