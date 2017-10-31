"""GraphQL schema extensions for the Student Dashboard."""

import logging
import os

import graphene
import graphene.relay
import graphql
from graphql_relay.node import node as graphql_node


import appengine_config
from common import utils as common_utils
from controllers import sites
from models import custom_modules
from modules.courses import constants, graphql as courses_graphql
from modules.explorer import graphql as explorer_graphql
from modules.gql import gql


class PrivateLesson(gql.Lesson):
    progress = graphene.String()
    link = graphene.String()

    def __init__(self, app_context, unit, lesson,
                 lesson_progress=None, link=None, **kwargs):
        super(PrivateLesson, self).__init__(
            app_context, unit, lesson, **kwargs)
        self._lesson_progress = lesson_progress
        self._link = link

    def resolve_progress(self, args, info):
        return self._lesson_progress

    def resolve_link(self, args, info):
        return self._link

    @classmethod
    def get_lesson(cls, lesson_id):
        lesson = super(PrivateLesson, cls).get_lesson(lesson_id)
        _, unit_id, lesson_id = lesson_id.split(gql.ID_SEP)
        expanded_lesson = lesson.course_view.find_element([unit_id, lesson.id])
        if expanded_lesson:
            return cls(
                lesson.course.app_context, lesson._unit,
                lesson=expanded_lesson.course_element,
                lesson_progress=expanded_lesson.progress,
                link=expanded_lesson.link,
                course=lesson._course, course_view=lesson._course_view,
                id=lesson.id
            )
        else:
            return None

    @classmethod
    def get_detailed_lessons(cls, course, course_view, unit):
        return [
            cls.get_lesson(cls._get_lesson_id(course, unit, lesson))
            for lesson in course_view.get_lessons(unit.unit_id)]


class PrivateUnit(gql.Unit):
    all_lessons = graphene.relay.ConnectionField(PrivateLesson)
    lesson = graphene.Field(PrivateLesson, id=graphene.String())
    detailed_lessons = graphene.relay.ConnectionField(PrivateLesson)

    @classmethod
    def get_unit(cls, unit_id):
        unit = super(PrivateUnit, cls).get_unit(unit_id)
        if unit:
            return cls(
                unit.course.app_context, unit.unit,
                course=unit.course, course_view=unit.course_view,
                id=cls._get_unit_id(unit.course, unit.unit))
        else:
            return None

    @classmethod
    def get_all_units(cls, course, course_view):
        return [
            cls(
                course.app_context, unit,
                course=course, course_view=course_view,
                id=cls._get_unit_id(course, unit))
            for unit in course_view.get_units()
        ]

    def resolve_all_lessons(self, args, info):
        return PrivateLesson.get_all_lessons(
            self.course, self.course_view, self._unit)

    def resolve_lesson(self, args, info):
        try:
            lesson_id = gql._resolve_id(PrivateLesson, args['id'])
            return PrivateLesson.get_lesson(lesson_id)
        except:  # pylint: disable=bare-except
            logging.exception('Error resolving lesson')
            return None

    def resolve_detailed_lessons(self, args, info):
        return PrivateLesson.get_detailed_lessons(
            self.course, self.course_view, self._unit
        )


class PrivateCourse(gql.Course):
    all_units = graphene.relay.ConnectionField(PrivateUnit)
    unit = graphene.Field(PrivateUnit, id=graphene.String())

    def resolve_all_units(self, args, info):
        return PrivateUnit.get_all_units(self.course, self.course_view)

    def resolve_unit(self, args, info):
        try:
            unit_id = gql._resolve_id(PrivateUnit, args['id'])
            return PrivateUnit.get_unit(unit_id)
        except:  # pylint: disable=bare-except
            logging.exception('Errors resolving unit')
            return None

    @classmethod
    def get_course(cls, course_id):
        app_context = sites.get_course_for_path(course_id)
        if not app_context or app_context.get_slug() != course_id:
            return None
        if cls._is_visible(app_context):
            return cls(app_context, id=app_context.get_slug())
        return None

    @classmethod
    def get_all_courses(cls):
        all_courses = []
        for app_context in sites.get_all_courses():
            if cls._is_visible(app_context):
                all_courses.append(cls(
                    app_context=app_context, id=app_context.get_slug()))
        return all_courses


class PrivateQuery(gql.Query):
    course = graphene.Field(PrivateCourse, id=graphene.String())
    all_courses = graphene.relay.ConnectionField(PrivateCourse)

    def resolve_course(self, args, info):
        try:
            course_id = gql._resolve_id(PrivateCourse, args['id'])
            return PrivateCourse.get_course(course_id)
        except:  # pylint: disable=bare-except
            common_utils.log_exception_origin()
            logging.exception('Error resolving course')
            return None

    def resolve_all_courses(self, args, info):
        try:

            return PrivateCourse.get_all_courses()
        except:  # pylint: disable=bare-except
            common_utils.log_exception_origin()
            raise


class PrivateGraphQLRestHandler(gql.GraphQLRestHandler):
    URL = '/modules/gql/query/v2'

    def _get_response_dict(self, query_str, expanded_gcb_tags):
        if not query_str:
            return {
                'data': None,
                'errors': ['Missing required query parameter "q"']
            }

        schema = graphene.Schema(query=PrivateQuery)
        try:
            result = schema.execute(
                request=query_str,
                request_context={
                    'handler': self,
                    'expanded_gcb_tags': expanded_gcb_tags,
                })
            for err in result.errors:
                logging.error('GraphQL schema.execute error: %s', err)
            return {
                'data': result.data,
                'errors': [err.message for err in result.errors]
            }
        except graphql.core.error.GraphQLError as err:
            if not appengine_config.PRODUCTION_MODE:
                log_level = logging.exception
            else:
                log_level = logging.error
            log_level('GraphQL error with query: %s', query_str)
            return {
                'data': None,
                'errors': [err.message]
            }


def register_resolvers():
    PrivateCourse.add_to_class(
        constants.START_DATE_SETTING,
        graphene.String(resolver=courses_graphql.resolve_start_date))
    PrivateCourse.add_to_class(
        constants.END_DATE_SETTING,
        graphene.String(resolver=courses_graphql.resolve_end_date))


def register():
    PrivateQuery.add_to_class(
        'site', graphene.Field(explorer_graphql.Site,
                               resolver=explorer_graphql.resolve_site))

    PrivateCourse.add_to_class(
        'estimated_workload', graphene.String(
            resolver=explorer_graphql.resolve_estimated_workload))

    PrivateCourse.add_to_class(
        'category', graphene.Field(explorer_graphql.CourseCategory,
                                   resolver=explorer_graphql.resolve_category))

    register_resolvers()
