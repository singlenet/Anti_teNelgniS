//
//  main.c
//  OpenSNet
//
//  Created by realityone on 15/10/24.
//  Copyright © 2015年 realityone. All rights reserved.
//

#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <getopt.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#include "SNAttributes.h"
#include "SNHeartBeat.h"
#include "SNConstants.h"
#include "SNNets.h"

#define DEFAULT_TIMEOUT {2, 0}

static const char short_opts[] = "u:i:I:t:P:h";
static struct option long_options[] = {
    {"username", required_argument, NULL, 'u'},
    {"ip", required_argument, NULL, 'i'},
    {"interval", required_argument, NULL, 'I'},
    {"target", required_argument, NULL, 't'},
    {"port", required_argument, NULL, 'P'},
    {"help", no_argument, NULL, 'h'},
    {NULL, 0, NULL, 0}
};

static struct UserConfig {
    const char username[32];
    const char ipaddress[16];
    const char target[16];
    int port;
    int interval;
}user_config;

void print_usage() {
    fprintf(stdout, "Usage: OpenSNet [OPTIONS]\n");
    fprintf(stdout, "Options:\n");
    fprintf(stdout, "  --username,  -u:      Username.\n");
    fprintf(stdout, "  --ipaddress, -i:      IP Address.\n");
    fprintf(stdout, "  --interval,  -I:      Interval.\n");
    fprintf(stdout, "  --target,    -t:      Target.\n");
    fprintf(stdout, "  --port,      -P:      Port.\n");
    fprintf(stdout, "  --help,      -h:      Help.\n");
    exit(0);
}

void validate_config() {
    if (!strlen(user_config.username) ||
        !strlen(user_config.ipaddress) ||
        !strlen(user_config.target) ||
        !user_config.port ||
        !user_config.interval) {
        fprintf(stderr, "Missing arguments.\n");
        print_usage();
    }
}

void parse_args(int argc, const char * argv[]) {
    int opt;
    
    while ((opt = getopt_long(argc, (char *const *)argv, short_opts, long_options, NULL)) != -1) {
        switch (opt) {
            case 'h':
                print_usage();
                break;
                
            case 'u':
                strcpy((char *)user_config.username, optarg);
                break;
                
            case 'i':
                strcpy((char *)user_config.ipaddress, optarg);
                break;
                
            case 't':
                strcpy((char *)user_config.target, optarg);
                break;
                
            case 'P':
                user_config.port = atoi(optarg);
                break;
                
            case 'I':
                user_config.interval = atoi(optarg);
                break;
                
            default:
                print_usage();
                break;
        }
    }
    validate_config();
}

void main_loop(int argc, const char * argv[]) {
    int times;
    int sockfd;
    int result;
    time_t timestamp;
    size_t packet_len;
    char *keepalive_data;
    SNHeartBeat ThunderProtocol;
    struct sockaddr_in target_addr;
    struct timeval timeout = DEFAULT_TIMEOUT;
    
    parse_args(argc, argv);
    
    sockfd = udp_init(user_config.target, user_config.port, &target_addr);
    udp_set_timeout(sockfd, timeout);
    
    times = 0;
    while (1) {
        times += 1;
        timestamp = time(NULL);
        keepalive_data = calc_keepalive_data(timestamp);
        packet_len = sn_thunderprotocol(user_config.username, user_config.ipaddress,
                                        timestamp, CLIENT_VERSION, keepalive_data, &ThunderProtocol);
        packet_len = generate_send_data(timestamp, &ThunderProtocol);
        if ((result = (int)udp_sendto(sockfd, &target_addr, (u_char *)&ThunderProtocol, packet_len)) > 0) {
            fprintf(stdout, "INFO: Send packet succeed.\n");
            bzero(&ThunderProtocol, sizeof(SNHeartBeat));
            if ((result = (int)udp_rcvfrom(sockfd, (u_char *)&ThunderProtocol, packet_len)) > 0) {
                fprintf(stdout, "INFO: Recv packet succeed.\n");
            } else {
                fprintf(stderr, "ERROR: Wait for packet timeout.\n");
            }
        } else {
            fprintf(stderr, "ERROR: Send packet failed.\n");
        }
        fprintf(stdout, "INFO: Wait %d seconds.\n", user_config.interval);
        sleep(user_config.interval);
    }
}

int main(int argc, const char * argv[]) {
    main_loop(argc, argv);
    return 0;
}
