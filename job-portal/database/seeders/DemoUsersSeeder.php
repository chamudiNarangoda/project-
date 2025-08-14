<?php

namespace Database\Seeders;

// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class DemoUsersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        User::updateOrCreate(
            ['email' => 'admin@example.com'],
            [
                'name' => 'Admin User',
                'password' => Hash::make('password'),
                'role' => 'admin',
            ]
        );

        User::updateOrCreate(
            ['email' => 'recruiter@example.com'],
            [
                'name' => 'Recruiter User',
                'password' => Hash::make('password'),
                'role' => 'recruiter',
            ]
        );

        User::updateOrCreate(
            ['email' => 'seeker@example.com'],
            [
                'name' => 'Job Seeker User',
                'password' => Hash::make('password'),
                'role' => 'job_seeker',
            ]
        );
    }
}
