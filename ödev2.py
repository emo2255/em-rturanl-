import cv2
import numpy as np

# Kamera başlatm
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Orijinal görüntüyü bir kopyasını saklama
    original_frame = frame.copy()

    # RGB'den HSV'ye dönüşüm
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Yeşil ve mavi renkler için HSV aralıkları
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # Yeşil ve mavi maskeleri oluşturma
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Yeşil ve mavi renkleri beyaza dönüştürme
    frame[(mask_green != 0) | (mask_blue != 0)] = [255, 255, 255]

    # Kırmızı renk için genişletilmiş HSV aralığı
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Kırmızı renk maskeleri
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Kırmızı renk vurgusu
    red_highlight = cv2.bitwise_and(frame, frame, mask=mask_red)
    frame[(mask_red != 0)] = cv2.addWeighted(frame[(mask_red != 0)], 0.5, red_highlight[(mask_red != 0)], 0.5, 0)

    # Kırmızı haricindeki tüm renkleri siyaha dönüştürme
    frame[(mask_red == 0) & (mask_green == 0) & (mask_blue == 0)] = [0, 0, 0]

    # Modifiye edilmiş ve orijinal görüntüleri gösterme
    cv2.imshow('Modified Frame', frame)
    cv2.imshow('Original Frame', original_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
