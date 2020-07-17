#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:17:41 2020

@author: naivegiraffe
"""


import json
import datetime
import re

S1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
S0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"
def remove_accents(input_str):
    """Đổi các ký tự từ Uicode sang dạng không dấu và in thường
    Arguments:
        input_str {str} -- string cần chuyển đổi
    Returns:
        str -- string nếu chuyển đổi thành công
        None - otherwise
    """

    if input_str is None:
        return 'none'

    s = ""
    for c in input_str:
        if c in S1:
            s += S0[S1.index(c)]
        else:
            s += c
    return s.lower()


def is_date_2(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        return False
    
def is_date_11(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%Y')
        return True
    except ValueError:
        return False

def is_date_12(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m')
        return True
    except ValueError:
        return False

with open('data_fullcontent.json', encoding="utf-8") as json_file:
    data = json.load(json_file)


                                
    ####
    # list các keyword cần check, ở dạng lower và không dấu vì check trên str đã remove_accents()
    ####
    
    # có trường hợp viết tắt như 'mtg' thì không phải 'mt' nên 'mt' sẽ được thành 'mt '
    position_street_1 = ['mat tien', 'mot mat tien', 'mt ', '1 mat tien', '1mt', '1 mt']
    
    # có trường hợp content chứa '1800m2 mat tien', nghĩa là diện tích + mặt tiền.
    # nếu chỉ xét '2 mat tien' có thể bị sai nên em cách ra thành check ' 2 mat tien'
    # tương tự với tất cả trường hợp có '2' ở đầu
    
    
    position_street_2 = ['hai mat tien', 'ba mat tien', ' 2 mat tien', '3 mat tien', ' 2mt', '3mt', ' 2 mt', '3 mt']
    position_street_4 = [' 2 mt hem',  'mat tien hem', ' 2 mat hem', 'mot mat hem', 'mt hem', '1 mt hem', '1mth', '2mth']
    

    f_1 = []
    f_2 = []
    f_3 = []
    f_4 = []
    
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    
    for p in data:
        # O(1)
        
        for i in position_street_1:
            if i in remove_accents(p['content']):
                count_1 = count_1 + 1
                
        for i in position_street_2:
            if i in remove_accents(p['content']):
                count_2 = count_2 + 1

        for i in position_street_4:
            if i in remove_accents(p['content']):
                count_4 = count_4 + 1
                
        flag_s = False
        
        # 2 sec
        flag_s2 = False
        
        s2 = re.findall(r'[+-]?\d+/[+-]?\d+/[+-]?\d+', p['content'])
        if s2 != []:
            for i in s2:
                if is_date_2(i):
                    continue
                else:
                    flag_s2 = True
            
            if(flag_s2 == True):
                count_4 = count_4 + 1
                flag_s = True
                flag_s2 = False

                
        # 1 sec
        flag_s1 = False
        list_wk = ['24/7', '24/24', '1/500', '80/20']   
        
        s1 = re.findall(r'[+-]?\d+/[+-]?\d+', p['content'])
        if s1 != []:
            for i in s1:
                if is_date_11(i) or is_date_12(i):
                    continue
                elif i in list_wk:
                    continue
                elif len(i.split('/')[1]) > 3:
                    continue
                else:
                    print(i)
                    flag_s1 = True
            
            if(flag_s1 == True):
                count_3 = count_3 + 1
                flag_s = True
                flag_s1 = False
      
        
        # 0 sec
        if flag_s == False:
            list_addr = []
            for i in range(0, len(p['attributes'])):
                if p['attributes'][i]['type'] == 'addr_street':
                    list_addr.append(p['attributes'][i]['content'])
            if (len(list_addr) > 0):
                count_1 = count_1 + 1
                        
                
        # Đơn giản là xét ngược xuống, vì:
        #
        # nếu đã có 'hai mat tien' thì chắc chắn nó sẽ là position_street = 2
        # trong 'hai mat tien' cũng có 'mat tien' nhưng vì đã thuộc position_street = 2 (đúng)
        # nên nó không còn thuộc position_street = 1 (sai) nữa
        #
        # các trường hợp đặc biệt như content rao bán cùng lúc nhiều nhà, vừa có nhà position_street = 1
        # vừa có nhà position_street = 2 em đã hỏi trong file excel, ví dụ id = 120251
        
        
        # Chưa xét / tên đường, sẽ trình bày sau trong buổi meet
        
        if (count_4 > 0):
            entry = {'position_street': 4}
            p.update(entry)
            f_4.append(p['id'])
            
        elif (count_2 > 0):
            entry = {'position_street': 2}
            p.update(entry)
            f_2.append(p['id'])
            
        elif (count_3 > 0):
            entry = {'position_street': 3}
            p.update(entry)
            f_3.append(p['id'])
            
        elif (count_1 > 0):
            entry = {'position_street': 1}
            p.update(entry)
            f_1.append(p['id'])
            
        ####
        

                
        
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        
    
    print('position_street = 1', len(f_1), '\n')
    print('position_street = 2', len(f_2), '\n')
    print('position_street = 3', len(f_3), '\n')
    print('position_street = 4', len(f_4), '\n')
            
# Xuất ra lại một file mới có thêm thuộc tính 'position_street'
with open('data_fullcontext_new.json', 'w', encoding='utf8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)