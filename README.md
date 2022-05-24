# WarehouseTools
This repository contains tools for Raseko lending application. With those tools you can create and print student cards and product catalog pages.

From the repository you can find Python source files, documentation and installers for the tool set. Most important files are in the following table:

| File name | Purpose |
|---|---|
productPicture.py | Source code for creating product catalog pages
productPicture.ui | Qt Designer file for the UI of catalog page tool
productPictureSettings.dat | JSON based settings file for product catalog application. Used for camera and folder settings.
productPicture.spec | Build settings for the product catalog tool
studentCardv2.py | Source code for creating student cards
studentCardv2.ui | Qt Designer file for student card tool
studentCardv2.spec | Build settings for student card tool
studentPicture.py | Source code for webcamera tool which takes still pictures for the student card
studentPicture.ui | Qt Designer file for the webcamera tool
studentPictureSettings.dat |  JSON based settings file for student photo application. Used for camera and folder settings.
studentPicture.spec | Build settings for student photo taking tool
code128Bcode | Module for generating barcodes with the Libre barcode 128 font
Omakuva2.png | A placeholder image for the student card tool
Raseko-logo-vaaka.png | RASEKO's logo for the student card

## Product Catalog Tool

This tool is for creating quarter of the product catalog page. Every page consist of 4 rectangels showing a product picture, name of the product and the barcode. Tools saves this information into a pdf file. Catalog pages are created with Inkscape application and printed for a catalog stand.

![image](https://user-images.githubusercontent.com/24242044/170026343-726bc5d4-f182-451d-9f8d-a704fc72058b.png)

This is what a catalog page looks like:

![33666](https://user-images.githubusercontent.com/24242044/170033080-1586f793-a23f-4b9d-8ae5-1684fd411eba.jpg)


## Student Card Tool

This tools allows printing student cards using photos taken with student photo tool.

![image](https://user-images.githubusercontent.com/24242044/170027259-51607205-f17e-4fa5-9b48-db46a2a03762.png)

## Student Photo tool

This is a simple tool for taking student photographs with a webcam. The UI has same settings component as Product Catalog Tool, but it has not been implemented yet.

![image](https://user-images.githubusercontent.com/24242044/170027658-5979a2aa-4a61-4b5c-af62-13f972f7862c.png)
