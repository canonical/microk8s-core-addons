use_addon_manifest() {
    # Perform an action (apply or delete) on a manifest.
    # Optionally replace strings in the manifest
    #
    # Parameters:
    # $1 the name of the manifest. Should be in the addons directory and should not
    #    include the trailing .yaml eg ingress, dns
    # $2 the action to be performed on the manifest, eg apply, delete
    # $3 (optional) an associative array with keys the string to be replaced and value what to
    #    replace with. The string $ARCH is always injected to this array.
    #
    local manifest="$1.yaml"; shift
    local action="$1"; shift
    if ! [ "$#" = "0" ]
    then
        eval "declare -A items="${1#*=}
    else
        declare -A items
    fi
    local tmp_manifest="${SNAP_USER_DATA}/tmp/temp-$$.yaml"
    items[\$ARCH]=$(arch)

    mkdir -p ${SNAP_USER_DATA}/tmp
    SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
    cp "${SCRIPT_DIR}/../${manifest}" "${tmp_manifest}"
    for i in "${!items[@]}"
    do
        "$SNAP/bin/sed" -i 's@'$i'@'"${items[$i]}"'@g' "${tmp_manifest}"
    done
    "$SNAP/kubectl" "--kubeconfig=$SNAP_DATA/credentials/client.config" "$action" -f "${tmp_manifest}"
    use_manifest_result="$?"
    rm "${tmp_manifest}"
}

# Function to convert an IP address to a decimal number
ip_to_decimal() {
    local ip="$1"
    echo $(( $(echo "$ip" | awk -F'.' '{print ($1*256^3)+($2*256^2)+($3*256^1)+$4}') ))
}

# Function to convert a decimal number to an IP address
decimal_to_ip() {
    local decimal="$1"
    echo "$(( (decimal >> 24) & 255 )).$(( (decimal >> 16) & 255 )).$(( (decimal >> 8) & 255 )).$(( decimal & 255 ))"
}

# Function to validate if an IP address is within the CIDR range
ip_in_cidr() {
    local ip="$1"
    local cidr="$2"

    local cidr_ip=$(echo "$cidr" | cut -d'/' -f1)
    local cidr_mask=$(echo "$cidr" | cut -d'/' -f2)

    local ip_decimal=$(ip_to_decimal "$ip")
    local cidr_ip_decimal=$(ip_to_decimal "$cidr_ip")

    local bitmask=$((2**(32-cidr_mask)-1))
    local network_ip_decimal=$((cidr_ip_decimal & ~bitmask))

    local cidr_start_decimal=$((network_ip_decimal + 1))
    local cidr_end_decimal=$((network_ip_decimal + bitmask - 1))

    [ $ip_decimal -ge $cidr_start_decimal ] && [ $ip_decimal -le $cidr_end_decimal ]
}

# Function to choose a random valid IP address from the CIDR range
choose_random_ip() {
    local cidr="$1"
    local ip
    local count=0
    local max_attempts=100

    local cidr_ip=$(echo "$cidr" | cut -d'/' -f1)
    local base_ip="${cidr_ip%.*}."

    while [ "$count" -lt "$max_attempts" ]; do
        ip=$(shuf -i 1-254 -n 1)
        chosen_ip="${base_ip}$ip"

    if ip_in_cidr "$chosen_ip" "$cidr"; then
        echo "$chosen_ip"
        return 0
    fi

    ((count++))
    done

    echo "Failed to find a valid IP address after $max_attempts attempts."
    return 1
}
