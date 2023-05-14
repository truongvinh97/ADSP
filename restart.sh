#!/bin/bash

# Thời gian đợi giữa các lần kiểm tra kết nối (đơn vị: giây)
WAIT_TIME=600

while true; do
  # Kiểm tra kết nối mạng bằng cách ping đến một địa chỉ IP bất kỳ
  if ping -c 1 8.8.8.8 &> /dev/null; then
    echo "Network connection is OK"
  else
    echo "Network connection is down. Restarting..."
    # Khởi động lại Raspberry Pi bằng lệnh reboot
    reboot
  fi

  # Kiểm tra kết nối Firebase bằng cách truy vấn một node bất kỳ trong Firebase
  if firebase database:get /connection/status &> /dev/null; then
    echo "Firebase connection is OK"
  else
    echo "Firebase connection is down. Restarting..."
    # Khởi động lại Raspberry Pi bằng lệnh reboot
    reboot
  fi

  # Đợi một khoảng thời gian trước khi kiểm tra lại
  sleep $WAIT_TIME
done