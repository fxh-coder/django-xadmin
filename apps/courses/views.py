from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from courses.models import Course, CourseTag, CourseResource, Video
from operations.models import UserFavorite, UserCourse, CourseComments, UserMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class VideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(
            user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_courses = UserCourse.objects.filter(
            user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(
            user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(
            user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(
            user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

            user_message = UserMessage()
            user_message.user = request.user
            user_message.message = "欢迎您加入{}这门课程，赶快来学习吧！".format(course.name)
            user_message.save()


        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_courses = UserCourse.objects.filter(
            user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)
        
        unread_nums = UserMessage.objects.filter(has_read=False).count()

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "unread_nums": unread_nums
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 通过课程的tag做课程的推荐(模糊查询：name__contains 或者 name__iconcontains 区别是大小感敏感)
        # 如果我们是想要对一批数据进行过滤的话，就需要exclude(id__in=[...])将需要过滤的添加到[]中
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag__contains=tag).exclude(id=course.id)[:3]

        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(
            tag__in=tag_list).exclude(course__id=course.id)
        # 使用set避免多个标签符合要求而被重复添加
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        user_courses = course.usercourse_set.all()[:3]
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
            "user_courses": user_courses
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        # 搜索关键词
        keywords = request.GET.get('keywords', "")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(
                desc__icontains=keywords) | Q(detail__icontains=keywords))

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 对课程数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=5, request=request)

        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "keywords": keywords,
            "s_type": s_type
        })
