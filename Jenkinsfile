/* 
* Copyright (c) 2017 and Confidential to Pegasystems Inc. All rights reserved.  
*/ 

pipeline {
    agent any

    options {
      timestamps()
      timeout(time: 15, unit: 'MINUTES')
      withCredentials(bindings: [usernamePassword(credentialsId: 'imsadmin', usernameVariable: 'IMS_USER', passwordVariable: 'IMS_PASSWORD')])
    }
    stages {
        stage('Creating virtualenv'){
            steps{
                sh '''#!/bin/bash
                virtualenv -p python3 venv &> /dev/null
                . venv/bin/activate venv &> /dev/null
                pip3 install -r requirements.txt
                '''
            }
        }
        stage('Check for merge conflicts'){
            steps {
                echo 'Determine Conflicts'
                sh '''. venv/bin/activate venv &> /dev/null
                python3 ./getConflict.py ${PEGA_DEV} ${branchName} ${applicationName} ${applicationVersion}'''
            }
        }
    }
}