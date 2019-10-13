#importing PyOTA library to interact with
import iota as i # pip install pyota[ccurl]
import json

nodeURL = "https://nodes.thetangle.org"
api = i.Iota(nodeURL) # selecting IOTA node
tag = "999ARPB9HSRW"

class IotaHandler():  
    def str_to_tryte(self, message):
        message_trytes = i.TryteString.from_unicode(str(message))
        return message_trytes

    # generate transaction object
    def get_prop_transaction(self, msg, adr, tag=tag):
        _ptx = i.ProposedTransaction(
            address=i.Address(adr),
            value=0,
            tag=tag,
            message=msg
        )
        return _ptx

    # send transaction object to tangle
    def send_transaction(self, ptx):
        bundle = api.send_transfer(
            depth=3,
            min_weight_magnitude=14,
            transfers=[ptx]
        )
        return bundle
    
    def data_to_tangle(self, addr, json_data):
        message_json_trytes = self.str_to_tryte(json_data)
        try:
            bundle = self.send_transaction(self.get_prop_transaction(msg=message_json_trytes, adr=addr))
            print("Transaction:\t https://thetangle.org/transaction/{0}\n".format(bundle['bundle'][0].hash))
        except Exeception as e:
            print(e)