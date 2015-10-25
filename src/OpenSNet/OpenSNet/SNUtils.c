//
//  SNUtils.c
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#include "SNUtils.h"

void int2byte(int num, u_char *output) {
    int i;
    for (i = 0; i < 4; i++) {
        output[i] = (u_char)(num >> (8 * (3 - i)) & 0xFF);
    }
}

void byte2str(u_char *byte_arr, size_t byte_len, char *output) {
    static char hex[] = "0123456789abcdef";
    char *pout = output;
    
    int i;
    for (i = 0; i < byte_len; i++, pout += 2) {
        pout[0] = hex[byte_arr[i] >> 4 & 0xF];
        pout[1] = hex[byte_arr[i] & 0xF];
    }
    
    pout[0] = '\0';
}