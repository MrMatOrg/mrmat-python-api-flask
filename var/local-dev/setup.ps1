#
# Set up a local dev environment

#
# Variables
# If we are running docker with HyperV then $WSL_PG_DATADIR = $HOST_PG_DATADIR.
# If we are running with WSL2 then the path must be changed to match where it is
# mounted from within WSL2

$INFRA_NETWORK = "infra"
$CONTAINER_POSTGRES="postgres:13.3-buster"
$CONTAINER_KEYCLOAK="quay.io/keycloak/keycloak:15.0.0"
$PG_DBNAME=($Env:COMPUTERNAME).ToLower() + "db"
$PG_PASSWORD="verysecret"
$KEYCLOAK_PASSWORD="verysecret"
$HOST_PG_DATADIR="$($Env:USERPROFILE)\var\pg\data"
$WSL_PG_DATADIR=$HOST_PG_DATADIR.Replace("\", "/").Replace(":","").ToLower()
$HOST_PG_INITDIR="$($Env:USERPROFILE)\var\pg\init"
$WSL_PG_INITDIR=$HOST_PG_INITDIR.Replace("\", "/").Replace(":","").ToLower()
$LOCAL_SCRIPTDIR="$($PSScriptRoot)\pg-init-scripts"

#
# Create a dedicated docker network if it doesn't already exist

$networks = docker network ls
if($networks -Match " $INFRA_NETWORK ") {
    Write-Host "Docker network $INFRA_NETWORK already exists"
} else {
    Write-Host "Creating docker network $INFRA_NETWORK"
    docker network create $INFRA_NETWORK | Out-Null
}

#
# Make sure we have data and init directories for pg

New-Item -Force -Path $HOST_PG_DATADIR -ItemType Directory | Out-Null
New-Item -Force -Path $HOST_PG_INITDIR -ItemType Directory | Out-Null

#
# Copy the init scripts into the initdir
# Note: We explicitly wish to fail before overwriting something

Write-Host $LOCAL_SCRIPTDIR
Copy-Item -Path "$($LOCAL_SCRIPTDIR)\*" -Destination $HOST_PG_INITDIR -Recurse 

#
# Start the PostgreSQL container

$containers = docker ps -a
if($containers -Match " pg") {
    Write-Host "A container with the name pg already exists"
} else {
    docker run -d `
        --name pg `
        --net infra `
        -e POSTGRES_PASSWORD="$PG_PASSWORD" `
        -e POSTGRES_DB="$PG_DBNAME" `
        -e PGDATA=/var/lib/postgresql/data/pgdata `
        -v "$($WSL_PG_DATADIR):/var/lib/postgresql/data" `
        -v "$($WSL_PG_INITDIR):/docker-entrypoint-initdb.d:ro" `
        -p 127.0.0.1:5432:5432/tcp `
        $CONTAINER_POSTGRES | Out-Null
}

#
# Start the Keycloak container

if($containers -Match " keycloak") {
    Write-Host "A container with the name keycloak already exists"
} else {
    docker run -d `
        --name keycloak `
        --net infra `
        -e DB_VENDOR="postgres" `
        -e DB_ADDR="pg" `
        -e DB_PORT="5432" `
        -e DB_SCHEMA="keycloak" `
        -e DB_DATABASE="$PG_DBNAME" `
        -e DB_USER="keycloak" `
        -e DB_PASSWORD="keycloak" `
        -e KEYCLOAK_USER="admin" `
        -e KEYCLOAK_PASSWORD="$KEYCLOAK_PASSWORD" `
        -p 127.0.0.1:8080:8080/tcp `
        $CONTAINER_KEYCLOAK | Out-Null
}