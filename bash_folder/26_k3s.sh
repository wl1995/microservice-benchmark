echo "k3s launched: $(date +"%T.%N")"  > /home/tumi6/workspace/autoware-microservice-bench/autoware_log/26_log.txt
sudo kubectl apply -f /home/tumi6/workspace/autoware-microservice-bench/wcm_k3s_deployments/wcm-final.yaml
