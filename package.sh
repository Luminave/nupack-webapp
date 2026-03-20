#!/bin/bash
# 打包脚本

cd ~
tar -czvf nupack-webapp.tar.gz nupack-webapp-release/
echo ""
echo "✅ 打包完成: ~/nupack-webapp.tar.gz"
echo "大小: $(du -h ~/nupack-webapp.tar.gz | cut -f1)"
