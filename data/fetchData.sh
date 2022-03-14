#!/bin/bash

urls=("https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2014-f040e0.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2015-69fdf0.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2016-912f00.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2017-d4d086.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2018-96034e.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2019-33ea73.zip" "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontrealrentals2020-8e67d9.zip")
files=("bixi2014.zip" "bixi2015.zip" "bixi2016.zip" "bixi2017.zip" "bixi2018.zip" "bixi2019.zip" "bixi2020.zip")

for n in {0..6};
do
    curl -sS ${urls[n]} > ${files[n]}
    echo ${files[n]}
    unzip ${files[n]}
    rm ${files[n]}
done