# Strategy for the IEEE Very Small Size Soccer (VSSS) category using Deep Reinforcement Learning

## Run unit tests
python3 -m unittest <test_file_relative_path>

## Create protobuf messages source code
protoc --proto_path=communication/protobuf/firasim/proto --python_out=communication/protobuf/firasim communication/protobuf/firasim/proto/*.proto

## FIRASim
https://github.com/VSSSLeague/FIRASim

## VSSReferee
https://github.com/VSSSLeague/VSSReferee

## Legacy repository
https://github.com/victorhac/futebol_robos_laser_gym_utfpr