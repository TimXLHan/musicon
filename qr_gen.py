import qrcode

# Create a QRCode object with the desired information
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data("temp")
qr.make(fit=True)

# Create an image from the QRCode object
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the image
qr_image.save("temp_qrcode.png")
