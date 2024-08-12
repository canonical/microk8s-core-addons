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

    # extract the part-of label value
    local part_of_label
    part_of_label=$(echo "$manifest" | cut -d'/' -f1)

    # insert label app.kubernetes.io/part-of
    # for all resources
    yq eval-all "
      .metadata.labels |= (. // {}) |
      .metadata.labels[\"app.kubernetes.io/part-of\"] = \"$part_of_label\"
    " -i "${tmp_manifest}"

    "$SNAP/kubectl" "--kubeconfig=$SNAP_DATA/credentials/client.config" "$action" -f "${tmp_manifest}"
    use_manifest_result="$?"
    rm "${tmp_manifest}"
}
