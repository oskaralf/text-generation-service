/*
  Warnings:

  - You are about to drop the `Interest` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `_UserInterests` table. If the table is not empty, all the data it contains will be lost.

*/
-- AlterTable
ALTER TABLE "User" ADD COLUMN "interests" TEXT;

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Interest";
PRAGMA foreign_keys=on;

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "_UserInterests";
PRAGMA foreign_keys=on;
