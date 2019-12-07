pipeline{
        agent any
        
        stages{
                stage('--Install service script and stop old service--'){
                        steps{
                                sh '''ssh 35.233.83.43 << BOB
                                      git clone https://github.com/devops-cohort/amogh.git
                                      cd amogh/
                                      sudo cp flask-app.service /etc/systemd/system/
                                      sudo systemctl daemon-reload
                                      sudo systemctl stop flask-app
                                      '''
                        }
                }  
                stage('--Install application files--'){
                        steps{
                                sh '''ssh 35.233.83.43 << BOB
                                      install_dir=/opt/flask-app
                                      sudo rm -rf ${install_dir}
                                      sudo mkdir ${install_dir}
                                      sudo cp -r ./* ${install_dir}
                                      sudo chown -R pythonadm:pythonadm ${install_dir}
                                      '''
                        }
                }
                stage('--Configure python virtual environment and install dependencies--'){
                        steps{
                                sh '''ssh 35.233.83.43 << BOB 
                                      sudo su - pythonadm << EOF
                                      cd ${install_dir}
                                      cd bookreviews/
                                      virtualenv -p python3 venv
                                      source venv/bin/activate
                                      pip install -r requirements.txt
                                      '''
                        }
                }
                stage('--testing--'){
                        steps{
                                sh '''ssh 35.233.83.43 << BOB
                                      pytest --cov --cov-report html
                                      mv ./htmlcov/index.html ./documentation/
                                      rm -rf ./htmlcov/
                                      EOF
                                      '''
                        }
                }
                stage('--deployment--'){
                        steps{
                                sh '''ssh 35.233.83.43 << BOB
                                      sudo systemctl start flask-app
                                      '''
                        }
                }
        }
}
