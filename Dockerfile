FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# 复制构建产物
COPY target/exchange-rate-*.jar app.jar

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# 启动命令
ENTRYPOINT ["java","-jar","-Xms256m","-Xmx512m","-Dspring.profiles.active=prod","app.jar"]
