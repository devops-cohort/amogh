pipeline{
        agent any
        
        stages{
                stage('--Install service script and stop old service--'){
                        steps{
                                sh '''ssh 35.205.131.101 << BOB
                                      rm -rf amogh/
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
                                sh '''ssh 35.205.131.101 << BOB
                                      sudo rm -rf /opt/flask-app
                                      sudo mkdir /opt/flask-app
                                      sudo cp -r ./* /opt/flask-app
                                      sudo chown -R pythonadm:pythonadm /opt/flask-app
                                      '''
                        }
                }
                stage('--Configure python virtual environment and install dependencies--'){
                        steps{
                                sh '''ssh 35.205.131.101 << BOB 
                                      sudo su - pythonadm << EOF
                                      cd /opt/flask-app/amogh/bookreviews
                             
                                      python3 -m virtualenv venv
                                      . venv/bin/activate
                                      pip3 install -r requirements.txt
                                      '''
                        }
                }
                stage('--testing--'){
                        steps{
                                sh '''ssh 35.205.131.101 << BOB
                                      sudo su - pythonadm << EOF
                                      cd /opt/flask-app/amogh/bookreviews
                                      . venv/bin/activate
                             
                                      python3 -m pytest --cov --cov-report html
                                      mv ./htmlcov/index.html ./documentation/
                                      rm -rf ./htmlcov/
                                     
                                      '''
                        }
                }
                stage('--deployment--'){
                        steps{
                                sh '''ssh 35.205.131.101 << BOB
                                      sudo systemctl start flask-app
                                      '''
                        }
                }
        }
}
