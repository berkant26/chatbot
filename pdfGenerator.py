from fpdf import FPDF
from unidecode import unidecode
def create_sample_manual_pdf(file_path="iphone.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    text = """
    Title: The Evolution and Features of the iPhone: A Comprehensive Guide

1. Introduction
The iPhone is Apple Inc.'s flagship smartphone line, first introduced by Steve Jobs in 2007. It revolutionized the mobile phone industry by combining a phone, an iPod, and an internet communicator into one device. Since then, the iPhone has undergone many changes and improvements across hardware, software, and design, becoming a staple of modern life and a cultural icon.

2. History of the iPhone

iPhone (2007): Introduced a multi-touch screen, virtual keyboard, and full HTML browser. It ran on iOS (then iPhone OS).

iPhone 3G and 3GS: Added 3G networking, GPS, and improved performance.

iPhone 4 and 4S: Introduced Retina display and the Siri voice assistant.

iPhone 5 Series: Larger screen, Lightning connector, LTE support.

iPhone 6 to SE (1st Gen): Larger display variants (4.7” and 5.5”), Touch ID, and A-series chip improvements.

iPhone X (2017): Removed the home button, introduced Face ID, and OLED display.

iPhone 11 to 14: Progressively enhanced cameras, chipsets (A13 to A15), battery life, and introduced features like Night Mode and Deep Fusion.

iPhone 15 Series (2023): First iPhone with USB-C port, Titanium frame in Pro models, and A17 Pro chip.

3. Key Features of Modern iPhones

Display: Super Retina XDR OLED displays with HDR10 and Dolby Vision support.

Camera System: Dual to triple-lens setups with wide, ultra-wide, and telephoto lenses. Advanced computational photography features such as Night Mode, Deep Fusion, and Smart HDR.

Processor: Apple’s A-series chips are industry-leading in performance and energy efficiency.

Operating System: iOS, updated annually, brings new features like App Library, Widgets, Live Text, and more.

Security: Face ID facial recognition, end-to-end encrypted messaging with iMessage, and privacy-focused settings.

Ecosystem Integration: Seamless connectivity with Apple Watch, iPad, Mac, and iCloud services.

5. Notable iOS Features for Users

App Store: Millions of apps for productivity, games, education, and health.

iCloud: Backup, file storage, and device sync.

Privacy Labels: Show what data apps collect before downloading.

Screen Time: Monitor and limit device usage.

Live Activities & Dynamic Island (Pro models): Real-time app updates on the lock screen and pill-shaped cutout.

6. Environmental and Accessibility Commitment

Apple emphasizes sustainability, using recycled materials and aiming for carbon neutrality. Accessibility features like VoiceOver, Magnifier, and AssistiveTouch help users with disabilities use the iPhone effectively.

7. Future of the iPhone

Apple continues to explore technologies like foldable displays, under-display Face ID, and satellite communication. The iPhone remains central to Apple’s product strategy, and its integration with AI and AR technologies is expected to grow.
    """
    text = unidecode(text)

    text = text.replace("–", "-")  # fix encoding issue
    for line in text.strip().split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(file_path)
    print(f"✅ PDF created: {file_path}")

# ✅ Call the function
create_sample_manual_pdf()
