//
//  SNAttribute.c
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#include <string.h>
#include <arpa/inet.h>
#include <mbedtls/md5.h>

#include "SNAttributes.h"
#include "SNConstants.h"
#include "SNUtils.h"

char *calc_keepalive_data(time_t timestamp) {
    static char keepalive_data[64];
    u_char timebytes[4];
    u_char md5_result[16];
    mbedtls_md5_context md5;
    
    if (strlen(keepalive_data) == 0) {
        strcpy(keepalive_data, DEFAULT_KEEPALIVE_DATA);
    }
    
    int2byte((int)timestamp, timebytes);
    
    mbedtls_md5_init(&md5);
    mbedtls_md5_starts(&md5);
    mbedtls_md5_update(&md5, timebytes, 4);
    mbedtls_md5_update(&md5, (const u_char *)keepalive_data, strlen(keepalive_data));
    mbedtls_md5_finish(&md5, md5_result);
    
    byte2str(md5_result, 16, keepalive_data);
    return keepalive_data;
}

size_t generate_attribute(u_char parent_id, u_char *attr_data, size_t attr_data_len, SNAttribute *output) {
    if (attr_data_len > MAX_ATTRIBUTE_DATA_LEN) {
        fprintf(stderr, "ERROR: Attribute data length is too long.");
        return -1;
    }
    
    bzero(output, sizeof(SNAttribute));
    
    output->parent_id = parent_id;
    output->length = attr_data_len;
    memcpy(output->data, attr_data, attr_data_len);
    
    return attr_data_len;
}

size_t sn_username(const char *username, SNAttribute *output) {
    return generate_attribute(USERNAME_ID, (u_char *)username, strlen(username), output);
}

size_t sn_cliet_ip_address(const char *ipaddress, SNAttribute *output) {
    in_addr_t ipaddr;
    u_char ip_bytes[4];
    
    ipaddr = ntohl(inet_addr(ipaddress));
    if (ipaddr == INADDR_NONE) {
        perror("ERROR:");
        return -1;
    }
    int2byte(ipaddr, ip_bytes);
    
    return generate_attribute(CLIENT_IPADDRESS_ID, ip_bytes, 4, output);
}

size_t sn_client_verison(const char *version, SNAttribute *output) {
    return generate_attribute(CLIENT_VERSION_ID, (u_char *)version, strlen(version), output);
}

size_t sn_keepalive_time(time_t timestamp, SNAttribute *output) {
    u_char timebytes[4];
    int2byte((int)timestamp, timebytes);
    
    return generate_attribute(KEEPALIVE_TIME_ID, timebytes, 4, output);
}

size_t sn_keepalive_data(const char *keepalive_data, SNAttribute *output) {
    return generate_attribute(KEEPALIVE_DATA_ID, (u_char *)keepalive_data, strlen(keepalive_data), output);
}

size_t mashup_attribtes_data(SNAttribute *attributes_array[], size_t arr_nums, u_char *output) {
    int i;
    size_t attr_data_len;
    size_t tmp_attr_data_len;
    u_char *poutput;
    
    poutput = output;
    for (i = 0; i < arr_nums; i++) {
        attr_data_len = attributes_array[i]->length + ATTRIBUTE_HEADER_LEN;
        tmp_attr_data_len = htons(attr_data_len);
        
        poutput[0] = attributes_array[i]->parent_id;
        memcpy(poutput + 1, &tmp_attr_data_len, sizeof(u_short));
        memcpy(poutput + ATTRIBUTE_HEADER_LEN, attributes_array[i]->data, attributes_array[i]->length);
        poutput += attr_data_len;
    }
    return poutput - output;
}
