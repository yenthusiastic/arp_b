Summary
----------

V1.0 

GET
----------

Test the get method by sending a htttp GET request to:

http://be.dev.iota.pw:5100/address/1


POST
----------

Test the post method by sending a http POST request to:

http://be.dev.iota.pw:5100/data

With the following data in JSON format:

{
	"hardwareID":"1",
	"address":"Postman_test",
	"latitude":"61.123",
	"longitude":"7.933",
	"temperature":"19.2",
	"humidity":"35.7",
	"timestamp":"2019-10-13 02:19:05.749277+02"
}