# Login
appcenter login --token bde06361b069a1d2f1d25739a9b973cb382adeff

# Show app list
appcenter apps list

# Show app deiails
appcenter apps show --app sergi.torrellas-soprasteria.com/We-Are-Nutrition

# Upload APK
appcenter distribute release --file /var/jenkins_home/app-production-release.apk  --app sergi.torrellas-soprasteria.com/We-Are-Nutrition -g Collaborators
