#!/bin/bash

# Environment variables for AWS CLI

#AWS_DEFAULT_REGION=
#AWS_REGION=

# CloudFormation aliases
alias stackls='aws cloudformation list-stacks --query "StackSummaries[*].[StackName, CreationTime, StackStatus]" --output text'
alias stackrm='aws cloudformation delete-stack --stack-name'

function stackpush() {
    local stack_name=$1
    local template_file=$2
    local parameters_file=$3

    # Deploy the CloudFormation stack with parameter overrides
    if [[ -z "$parameters_file" ]]; then
        aws cloudformation deploy --template-file "$template_file" \
            --stack-name "$stack_name" \
            --capabilities CAPABILITY_NAMED_IAM
    else
        aws cloudformation deploy --template-file "$template_file" \
            --stack-name "$stack_name" \
            --capabilities CAPABILITY_NAMED_IAM \
            --parameter-overrides file://"$parameters_file"
    fi
}

function stackrepush() {
    local stack_name=$1
    local template_file=$2
    local parameters_file=$3

    # Check if the stack exists and is in a rollback state
    local stack_status=$(aws cloudformation describe-stacks \
        --stack-name "$stack_name" \
        --query "Stacks[0].StackStatus" \
        --output text 2>/dev/null)

    if [[ "$stack_status" == "ROLLBACK_COMPLETE" ]]; then
        echo "Stack $stack_name is in $stack_status state. Deleting the stack..."
        aws cloudformation delete-stack --stack-name "$stack_name"
        aws cloudformation wait stack-delete-complete --stack-name "$stack_name"
        stackpush "$stack_name" "$template_file" "$parameters_file"
    else
        echo "Stack $stack_name already exists and is not in a ROLLBACK_COMPLETE state."
        return
    fi
}
