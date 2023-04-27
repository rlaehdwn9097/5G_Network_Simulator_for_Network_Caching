import config as cf
import content as ct

# First In First Out
def FIFO(network, BS_type, BS_id):
    c = network.requested
    if BS_type != 'NODE' and BS_type != 'CORE':
        selected_BS = network.getBS(BS_id)
        if selected_BS.storage.abletostore(c)==0: 
            if selected_BS.storage.isstored(c) == 0:
                while selected_BS.storage.abletostore(c) == 0:
                    selected_BS.storage.delFirstStored()
                selected_BS.storage.addContent(c)
        else:
            if selected_BS.storage.isstored(c) == 0:
                selected_BS.storage.addContent(c)
        
# Least Recently Used 
def LRU(network, BS_type, BS_id):
    c = network.requested
    if BS_type != 'NODE' and BS_type != 'CORE':
        selected_BS = network.getBS(BS_id)

        if selected_BS.storage.isstored(c):
            selected_BS.storage.delContent(c)
            selected_BS.storage.addContent(c)
        else:
            if selected_BS.storage.abletostore(c)==1:
                selected_BS.storage.addContent(c)
            else:
                while selected_BS.storage.abletostore(c) == 0:
                    selected_BS.storage.delFirstStored()
                selected_BS.storage.addContent(c)

        

# Least Frequently Used
def LFU(network, BS_type, BS_id):
    c = network.requested

    if BS_type != 'NODE' and BS_type != 'CORE':
        selected_BS = network.getBS(BS_id)
        
        if selected_BS.storage.isstored(c):
            c_index = selected_BS.storage.getindex(c)
            selected_BS.storage.content_req_cnt_list[c_index] += 1
        else:
            if selected_BS.storage.abletostore(c)==1:
                selected_BS.storage.addContent(c)
            else:
                while selected_BS.storage.abletostore(c)==0:
                    min_index = selected_BS.storage.content_req_cnt_list.index(min(selected_BS.storage.content_req_cnt_list))
                    del_content = selected_BS.storage.content_storage[min_index]
                    selected_BS.storage.delContent(del_content)
                selected_BS.storage.addContent(c)
