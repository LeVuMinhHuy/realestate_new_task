## Phân loại position_street = 1, 2, 4
Kiểm tra trên tập `content` của mỗi post đã remove_accents
### Cách phân loại:
#### position_street = 1:
Xét các keyword     
`position_street_1 = ['mat tien', 'mot mat tien', 'mt ', '1 mat tien', '1mt', '1 mt']`

Note: chưa xét /

#### position_street = 2:
Xét các keyword     
`position_street_2 = ['hai mat tien', 'ba mat tien', ' 2 mat tien', '3 mat tien', ' 2mt', '3mt', ' 2 mt', '3 mt']`

#### position_street = 4:
Xét các keyword     
`position_street_4 = [' 2 mt hem',  'mat tien hem', ' 2 mat hem', 'mot mat hem', 'mt hem', '1 mt hem']`

### Kết quả:
#### file result:
`data_fullcontext_new.json`

#### len
Gọi f_1, f_2, f_4 là tập các id đã phân loại, ta có:
`len(f_1) = 595`
`len(f_2) = 105`
`len(f_4) = 10`
#### Các trường hợp đặc biệt:
- 120251: rao bán một lúc nhiều căn nhà, có cả '2 mặt tiền' và 'MT' của 2 căn nhà khác nhau. Vậy 'position_street' nên là 1 hay 2 hay là 1,2 ?

- 118236: "cách MT Lê Văn Việt", có MT nhưng không chăc là nhà mặt tiền, khả năng cao là trong hẻm

- ... đang kiểm tra thêm