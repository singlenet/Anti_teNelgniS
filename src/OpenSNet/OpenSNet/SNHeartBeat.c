//
//  SNHeartBeat.c
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#include <string.h>
#include <netinet/in.h>
#include <mbedtls/md5.h>

#include "SNHeartBeat.h"
#include "SNAttributes.h"
#include "SNConstants.h"


u_char calc_timecode(time_t timestamp) {
    int temp_num;
    temp_num = (int)(timestamp * 0x343FD + 0x269EC3);
    return (temp_num >> 0x10) & 0xFF;
}


size_t generate_heartbeat(u_char packet_id, time_t timestamp, u_char *attr_data,
                          size_t attr_data_len, SNHeartBeat *output) {
    size_t heartbeat_length;
    bzero(output, sizeof(SNHeartBeat));
    
    heartbeat_length = attr_data_len + HEARTBEAT_HEADER_LEN;
    
    output->magic_number = MAGIC_NUMBER;
    output->length = heartbeat_length;
    output->packet_id = packet_id;
    output->timecode = calc_timecode(timestamp);
    
    memcpy(output->attributes_data, attr_data, attr_data_len);
    return heartbeat_length;
}


void set_signature(time_t timestamp, SNHeartBeat *heartbeat, size_t heartbeat_len) {
    u_char md5_result[16];
    mbedtls_md5_context md5;
    
    mbedtls_md5_init(&md5);
    mbedtls_md5_starts(&md5);
    mbedtls_md5_update(&md5, (const u_char *)heartbeat, heartbeat_len);
    mbedtls_md5_update(&md5, (const u_char *)SIGNATURE_SLAT, strlen(SIGNATURE_SLAT));
    mbedtls_md5_finish(&md5, md5_result);
    
    memcpy(heartbeat->signature, md5_result, 16);
}


size_t sn_thunderprotocol(const char *username, const char *ipaddress, time_t timestamp,
                          const char *version, const char *keepalive_data, SNHeartBeat *output) {
    u_char attr_data[MAX_ATTRIBUTES_DATA_LEN];
    size_t attr_data_len;
    SNAttribute attr_client_ip_address;
    SNAttribute attr_client_version;
    SNAttribute attr_keepalive_data;
    SNAttribute attr_keepalive_time;
    SNAttribute attr_username;
    
    sn_cliet_ip_address(ipaddress, &attr_client_ip_address);
    sn_client_verison(version, &attr_client_version);
    sn_keepalive_data(keepalive_data, &attr_keepalive_data);
    sn_keepalive_time(timestamp, &attr_keepalive_time);
    sn_username(username, &attr_username);
    
    SNAttribute *(TP_Attributes[]) = {
        &attr_client_ip_address,
        &attr_client_version,
        &attr_keepalive_data,
        &attr_keepalive_time,
        &attr_username
    };
    
    attr_data_len = mashup_attribtes_data(TP_Attributes,
                                          sizeof(TP_Attributes) / sizeof(*TP_Attributes), attr_data);
    return generate_heartbeat(ThunderProtocolID, timestamp, attr_data, attr_data_len, output);
}

size_t generate_send_data(time_t timestamp, SNHeartBeat *heartbeat) {
    u_short length;

    length = heartbeat->length;
    heartbeat->magic_number = htons(heartbeat->magic_number);
    heartbeat->length = htons(heartbeat->length);
    
    set_signature(timestamp, heartbeat, length);
    return length;
}










