# ---- build stage ----
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /build

# dependencies first, so this layer stays cached while only src/ changes
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# ---- runtime stage ----
FROM eclipse-temurin:21-jre-latest
RUN addgroup -S spring && adduser -S spring -G spring
WORKDIR /app
COPY --from=build /build/target/*.jar app.jar
RUN chown spring:spring app.jar
USER spring
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75.0", "-jar", "/app/app.jar"]
