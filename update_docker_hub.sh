docker compose build
docker tag fit5020_onboarding_tp09-frontend:latest 7wikmonash/onb_fe
docker tag fit5020_onboarding_tp09-backend:latest 7wikmonash/onb_be
docker tag fit5020_onboarding_tp09-db:latest 7wikmonash/onb_db
# docker login
docker push 7wikmonash/onb_fe:latest 
docker push 7wikmonash/onb_be:latest
docker push 7wikmonash/onb_db:latest

## on cloud VM:
# docker compose pull
# docker compose up -d