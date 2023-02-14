#!/bin/sh
cd flask
minikube image build -t test_image .
