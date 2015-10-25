//
//  SNAttribute.h
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#ifndef SNAttribute_h
#define SNAttribute_h

#include <stdio.h>
#include <sys/types.h>

#define ATTRIBUTE_HEADER_LEN (sizeof(u_char) + sizeof(u_short))
#define MAX_ATTRIBUTE_DATA_LEN 128

#define USERNAME_ID 0x1
#define CLIENT_IPADDRESS_ID 0x2
#define CLIENT_VERSION_ID 0x3
#define KEEPALIVE_TIME_ID 0x12
#define KEEPALIVE_DATA_ID 0x14

typedef struct SNAttribute {
    u_char parent_id;
    u_short length;
    u_char data[MAX_ATTRIBUTE_DATA_LEN];
} SNAttribute;

char *calc_keepalive_data(time_t timestamp);

size_t generate_attribute(u_char parent_id, u_char *attr_data, size_t attr_data_len, SNAttribute *output);
size_t sn_username(const char *username, SNAttribute *output);
size_t sn_cliet_ip_address(const char *ipaddress, SNAttribute *output);
size_t sn_client_verison(const char *version, SNAttribute *output);
size_t sn_keepalive_time(time_t timestamp, SNAttribute *output);
size_t sn_keepalive_data(const char *keepalive_data, SNAttribute *output);

size_t mashup_attribtes_data(SNAttribute *attributes_array[], size_t arr_nums, u_char *output_data);

#endif /* SNAttribute_h */
