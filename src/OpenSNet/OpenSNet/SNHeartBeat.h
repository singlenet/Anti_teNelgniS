//
//  SNHeartBeat.h
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#ifndef SNHeartBeat_h
#define SNHeartBeat_h

#include <stdio.h>
#include <sys/types.h>

#define HEARTBEAT_HEADER_LEN (sizeof(u_short) + sizeof(u_short) + sizeof(u_char) + sizeof(u_char) + sizeof(u_char) * 16)
#define MAX_ATTRIBUTES_DATA_LEN 512
#define MAX_HEARTBEAT_LEN (HEARTBEAT_HEADER_LEN + MAX_ATTRIBUTES_DATA_LEN)

#define MAGIC_NUMBER 0x534E

#define ThunderProtocolID 0x3

typedef struct SNHeartBeat {
    u_short magic_number;
    u_short length;
    u_char packet_id;
    u_char timecode;
    u_char signature[16];
    u_char attributes_data[MAX_ATTRIBUTES_DATA_LEN];
} SNHeartBeat;

size_t generate_heartbeat(u_char packet_id, time_t timestamp, u_char *attr_data,
                          size_t attr_data_len, SNHeartBeat *output);

size_t sn_thunderprotocol(const char *username, const char *ipaddress, time_t timestamp,
                          const char *version, const char *keepalive_data, SNHeartBeat *output);

size_t generate_send_data(time_t timestamp, SNHeartBeat *heartbeat);
#endif /* SNHeartBeat_h */
