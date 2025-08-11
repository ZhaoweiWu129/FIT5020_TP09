docker compose build
docker tag fit5020_onboarding_tp09-frontend 7wikmonash/onb_fe
docker tag fit5020_onboarding_tp09-backend:latest 7wikmonash/onb_be
docker tag fit5020_onboarding_tp09-db 7wikmonash/onb_db
# docker login
docker push 7wikmonash/onb_fe:latest 
docker push 7wikmonash/onb_be:latest
docker push 7wikmonash/onb_db:latest

## on cloud VM:
# sudo docker pull 7wikmonash/onb_db
# sudo docker pull 7wikmonash/onb_be
# sudo docker pull 7wikmonash/onb_fe