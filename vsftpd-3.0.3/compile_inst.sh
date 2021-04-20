llc -filetype=obj  vsftpd_log.bc -o vsftpd.o
clang vsftpd.o -Wl,-s -fPIC -Wl,-z,relro -Wl,-z,now `./vsf_findlibs.sh` -o vsftpd

sudo make install
