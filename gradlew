#!/bin/sh

# Resolve APP_HOME
APP_HOME="$(cd "$(dirname "$0")" && pwd)"
export APP_HOME

# Determine Java command
if [ -n "$JAVA_HOME" ] && [ -x "$JAVA_HOME/bin/java" ]; then
    JAVACMD="$JAVA_HOME/bin/java"
elif [ -x "/data/data/com.termux/files/usr/lib/jvm/java-21-openjdk/bin/java" ]; then
    export JAVA_HOME="/data/data/com.termux/files/usr/lib/jvm/java-21-openjdk"
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

WRAPPER_JAR="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"

# If wrapper jar is present, use standard wrapper invocation
if [ -f "$WRAPPER_JAR" ]; then
    exec "$JAVACMD" "-Dorg.gradle.appname=gradlew" -jar "$WRAPPER_JAR" "$@"
fi

# Fallback: Check if system Gradle is installed in Termux
if command -v gradle >/dev/null 2>&1; then
    exec gradle "$@"
elif [ -x "/data/data/com.termux/files/usr/bin/gradle" ]; then
    exec /data/data/com.termux/files/usr/bin/gradle "$@"
fi

echo "ERROR: Neither gradle wrapper jar ($WRAPPER_JAR) nor system 'gradle' command was found." >&2
echo "Please run: 'pkg install gradle' in Termux or setup gradle wrapper." >&2
exit 1
