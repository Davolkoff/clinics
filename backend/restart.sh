# source venv/bin/activate
cd ../
docker compose down
docker compose up -d
cd backend
# rm -r media
echo 10 | { while read n; do
        sleep $n
    done
    wait
}
rm -r core/migrations
rm -r appointments/migrations
rm -r clinics/migrations
rm -r medical/migrations
rm -r reviews/migrations
rm -r services/migrations
rm -r users/migrations

python3 manage.py makemigrations core appointments clinics medical reviews services users
python3 manage.py migrate
python3 manage.py fill_db

python3 manage.py runserver