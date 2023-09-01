# Introduction

This is an example helm chart, please modify the readme to match your application.

## TL;DR;

```bash
helm repo add ncsa https://opensource.ncsa.illinois.edu/charts/
helm install simple ncsa/simple --set variable=testing
```

## Introduction

This chart is an example to show how to do a deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes 1.21+
- helm 3

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release ncsa/simple ---set variable=testing
```

The command deploys this helm chart on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation. 

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm uninstall my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the chart and their default values.

### Chart Options

A list of values frequently changed.

| Parameter                            | Description                                      | Default                                                 |
| ------------------------------------ | ------------------------------------------------ | -------------------------------------------------------|
| replicaCount | Number of replicas of the image to run | 1 |
| image.tag | Specific version of the image to run, default is the same as specified in the application version. | ""|
| persistence.existingClaim | Set this to not create a new claim, but use the existing claim | "" |
| persistence.size | Size of the claim that is created | 10Gi |
| persistence.storageClass | Specific storage class to use when creating the new PVC | "" |
| secrets.existingSecret | Set this to point to a secret, if an external secret should be used. This should contain the secret with the name `password`. | "" |
| secrets.password | Password that is used by the application. | "ncsa" |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```bash
helm install my-release ncsa/simple --set replicas=3
```

The above command sets the number of replicas to 3.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```bash
helm install my-release ncsa/simple -f myvalues.yaml
```

> **Tip**: You can use the default [values.yaml](values.yaml)

## Persistence

This simple application can use storage to hold the data. It will either create a new peristent volume, or you can use an existing volume.

### Existing PersistentVolumeClaims

1. Create the PersistentVolume
1. Create the PersistentVolumeClaim
1. Install the chart

```bash
helm install my-release ncsa/simple --set persistence.existingClaim=PVC_NAME
```

## Secrets

This simple application needs a secret to work. This secret should be set before installing the helm chart. You can either provide the secret as part of the helm chart install, or use an existing secret. Best is to use an existing secret that is set outside of the helm command.

