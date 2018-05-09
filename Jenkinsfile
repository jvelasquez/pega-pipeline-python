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

        stage('Check for merge conflicts'){
            steps {
                echo ('Clear workspace')
                dir ('build/export') {
                    deleteDir()
                }

                echo 'Determine Conflicts'
                sh "./getConflict.py ${PEGA_DEV} ${branchName} ${applicationName} ${applicationVersion}"
            }
        }
    }
}