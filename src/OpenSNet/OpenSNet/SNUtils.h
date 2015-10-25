//
//  SNUtils.h
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#ifndef SNUtils_h
#define SNUtils_h

#include <stdio.h>
#include <sys/types.h>

void int2byte(int num, u_char *output);
void byte2str(u_char *byte_arr, size_t byte_len, char *output);

#endif /* SNUtils_h */
