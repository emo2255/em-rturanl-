import cv2
import numpy as np

# Görüntüyü yükle
imagePath = "C:/Users/90538/desktop/rice.jpeg"
image = cv2.imread(imagePath)  # "pirinc.jpg" yerine kendi dosya adınızı kullanın
# Renkli görüntüyü gri tonlamalıya çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gürültüyü azaltmak için Gaussian Blur uygula
blurred = cv2.GaussianBlur(gray, (15, 15), 0)

# Eşikleme uygula
_, thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)

# Morfolojik işlemleri uygula
kernel = np.ones((5, 5), np.uint8)
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Etiketleme ve nesne sayısını bulma
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(morphed, connectivity=8)

# Görüntüdeki pirinç sayısı
rice_count = num_labels - 1  # Arka planı saymamak için

# Görüntüyü ekrana çiz
for i in range(1, num_labels):
    cv2.putText(image, f"Rice {i}", (int(centroids[i][0]), int(centroids[i][1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.circle(image, (int(centroids[i][0]), int(centroids[i][1])), 5, (0, 255, 0), -1)

cv2.imwrite("original_image.jpg", image)
cv2.imwrite("thresholded_image.jpg", thresh)
cv2.imwrite("morphed_image.jpg", morphed)

# Görüntü ve sayıları ekrana yazdır
cv2.imshow("Original Image", image)
cv2.imshow("Thresholded Image", thresh)
cv2.imshow("Morphed Image", morphed)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Pirinç sayısını konsola yazdır
print(f"Pirinç Sayısı: {rice_count}")
