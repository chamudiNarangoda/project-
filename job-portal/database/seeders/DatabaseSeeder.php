<?php

namespace Database\Seeders;

use App\Models\User;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Role;

class DatabaseSeeder extends Seeder
{
	/**
	 * Seed the application's database.
	 */
	public function run(): void
	{
		// Roles
		$roles = ['admin', 'recruiter', 'seeker'];
		foreach ($roles as $roleName) {
			Role::firstOrCreate(['name' => $roleName]);
		}

		// Admin user
		$admin = User::firstOrCreate(
			['email' => 'admin@example.com'],
			['name' => 'Admin', 'password' => bcrypt('password')]
		);
		$admin->syncRoles(['admin']);

		// Recruiter user
		recruiter:
		$recruiter = User::firstOrCreate(
			['email' => 'recruiter@example.com'],
			['name' => 'Recruiter', 'password' => bcrypt('password')]
		);
		$recruiter->syncRoles(['recruiter']);

		// Sample seeker
		$seeker = User::firstOrCreate(
			['email' => 'seeker@example.com'],
			['name' => 'Job Seeker', 'password' => bcrypt('password')]
		);
		$seeker->syncRoles(['seeker']);
	}
}
